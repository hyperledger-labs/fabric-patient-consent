# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import argparse
import asyncio
import logging
import os
from signal import signal, SIGINT
import sys
from sanic import Sanic

from sawtooth_signing import create_context
from sawtooth_signing import ParseError
from sawtooth_signing import CryptoFactory
from zmq.asyncio import ZMQEventLoop
from trial_rest_api.investigator import INVESTIGATORS_BP
from trial_rest_api.ehrs import EHRS_BP
from trial_rest_api.general import get_keyfile, get_signer_from_file
from trial_rest_api.clients import CLIENTS_BP
from sawtooth_rest_api.messaging import Connection


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
DEFAULT_CONFIG = {
    'HOST': 'localhost',
    'PORT': 8000,
    'TIMEOUT': 500,
    'TRIAL_VALIDATOR_URL': 'tcp://localhost:6004',
    'CONSENT_VALIDATOR_URL': 'tcp://localhost:5004',
    'EHR_BACKEND_URL': 'http://hospital-rest-api:8000',
    'DEBUG': True,
    'KEEP_ALIVE': False,
    'SECRET_KEY': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
    'AES_KEY': 'ffffffffffffffffffffffffffffffff',
    'BATCHER_PRIVATE_KEY': '1111111111111111111111111111111111111111111111111111111111111111',
    'BATCHER_PRIVATE_KEY_FILE_NAME_INVESTIGATOR': None
}


async def open_connections(appl):
    appl.config.INVESTIGATOR_VAL_CONN = Connection(appl.config.TRIAL_VALIDATOR_URL)
    appl.config.CONSENT_VAL_CONN = Connection(appl.config.CONSENT_VALIDATOR_URL)

    LOGGER.warning('opening validator connection for Investigator network: ' + str(appl.config.TRIAL_VALIDATOR_URL))
    LOGGER.warning('opening validator connection for Consent network: ' + str(appl.config.CONSENT_VALIDATOR_URL))

    appl.config.INVESTIGATOR_VAL_CONN.open()
    appl.config.CONSENT_VAL_CONN.open()


def close_connections(appl):
    LOGGER.warning('closing validator connection Investigator network')
    appl.config.INVESTIGATOR_VAL_CONN.close()
    LOGGER.warning('closing validator connection Consent network')
    appl.config.CONSENT_VAL_CONN.close()


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='The host for the api to run on.')
    parser.add_argument('--port',
                        help='The port for the api to run on.')
    parser.add_argument('--timeout',
                        help='Seconds to wait for a validator response')
    parser.add_argument('--trial-validator',
                        help='The url to connect to a running validator Trial network')
    parser.add_argument('--consent-validator',
                        help='The url to connect to a running validator Consent network')
    parser.add_argument('--ehr-backend',
                        help='The url to EHR backend')
    # parser.add_argument('--db-name',
    #                     help='The name of the database')
    parser.add_argument('--debug',
                        help='Option to run Sanic in debug mode')
    parser.add_argument('--secret_key',
                        help='The API secret key')
    parser.add_argument('--aes-key',
                        help='The AES key used for private key encryption')
    parser.add_argument('--batcher-private-key',
                        help='The sawtooth key used for transaction signing')
    parser.add_argument('--batcher-private-key-file-name-investigator',
                        help='The sawtooth key used for batch signing having investigator role')

    return parser.parse_args(args)


def load_config(appl):  # pylint: disable=too-many-branches
    appl.config.update(DEFAULT_CONFIG)
    config_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        'trial_rest_api/config.py')
    try:
        LOGGER.info('Path: ' + str(config_file_path))
        appl.config.from_pyfile(config_file_path)
    except FileNotFoundError:
        LOGGER.warning("No config file provided")

    # CLI Options will override config file options
    opts = parse_args(sys.argv[1:])

    if opts.host is not None:
        appl.config.HOST = opts.host
    if opts.port is not None:
        appl.config.PORT = opts.port
    if opts.timeout is not None:
        appl.config.TIMEOUT = opts.timeout

    if opts.trial_validator is not None:
        appl.config.TRIAL_VALIDATOR_URL = opts.trial_validator
    if opts.consent_validator is not None:
        appl.config.CONSENT_VALIDATOR_URL = opts.consent_validator
    if opts.ehr_backend is not None:
        app.config.EHR_BACKEND_URL = opts.ehr_backend
    # if opts.db_port is not None:
    #     app.config.DB_PORT = opts.db_port
    # if opts.db_name is not None:
    #     app.config.DB_NAME = opts.db_name

    if opts.debug is not None:
        appl.config.DEBUG = opts.debug

    if opts.secret_key is not None:
        appl.config.SECRET_KEY = opts.secret_key
    if appl.config.SECRET_KEY is None:
        LOGGER.exception("API secret key was not provided")
        sys.exit(1)

    if opts.aes_key is not None:
        appl.config.AES_KEY = opts.aes_key
    if appl.config.AES_KEY is None:
        LOGGER.exception("AES key was not provided")
        sys.exit(1)

    if opts.batcher_private_key is not None:
        appl.config.BATCHER_PRIVATE_KEY = opts.batcher_private_key
    if appl.config.BATCHER_PRIVATE_KEY is None:
        LOGGER.exception("Batcher private key was not provided")
        sys.exit(1)

    if opts.batcher_private_key_file_name_investigator is not None:
        appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_INVESTIGATOR = opts.batcher_private_key_file_name_investigator
    if appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_INVESTIGATOR is None:
        LOGGER.exception("Batcher private key file name for Data Provider entity was not provided")
        sys.exit(1)

    try:
        private_key_file_name_investigator = get_keyfile(appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_INVESTIGATOR)
        investigator_private_key = get_signer_from_file(private_key_file_name_investigator)
    except ParseError as err:
        LOGGER.exception('Unable to load private key: %s', str(err))
        sys.exit(1)
    appl.config.CONTEXT = create_context('secp256k1')
    appl.config.SIGNER_INVESTIGATOR = CryptoFactory(
        appl.config.CONTEXT).new_signer(investigator_private_key)


app = Sanic(__name__)
app.config['CORS_AUTOMATIC_OPTIONS'] = True


def main():
    LOGGER.info('Starting Hospital Rest API server...')
    # CORS(app)

    app.blueprint(INVESTIGATORS_BP)
    app.blueprint(EHRS_BP)
    app.blueprint(CLIENTS_BP)

    load_config(app)
    zmq = ZMQEventLoop()
    asyncio.set_event_loop(zmq)
    server = app.create_server(
        host=app.config.HOST, port=app.config.PORT, debug=app.config.DEBUG, return_asyncio_server=True)
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(open_connections(app))
    asyncio.ensure_future(server)
    signal(SIGINT, lambda s, f: loop.close())
    try:
        LOGGER.info('Hospital Rest API server starting')
        loop.run_forever()
    except KeyboardInterrupt:
        LOGGER.info('Hospital Rest API started interrupted')
        close_connections(app)
        loop.stop()


if __name__ == "__main__":
    main()

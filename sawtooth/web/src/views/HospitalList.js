var m = require("mithril")
var Hospital = require("../models/Hospital")
<<<<<<< HEAD
//var Investigator = require("../models/Investigator")
=======
>>>>>>> upstream/master

var qrcodeurl = ''

module.exports = {
    oninit:
        function(vnode){
            Hospital.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
//        return m(".user-list", Clinic.list.map(function(clinic) {
//            return m("a.user-list-item", clinic.name) // + " " + clinic.permissions)
//        }),
//        m("label.error", Clinic.error))
        return m(".user-list", Hospital.list.map(function(hospital) {
            return m("a.user-list-item", "PUBLIC KEY: " + hospital.public_key + "; NAME: " + hospital.name,
<<<<<<< HEAD
//                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + hospital.public_key + '&chld=H|0'
//                        }
//                    }, 'Generate QR code for Hospital Public Key: ' + hospital.public_key),
//                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            Hospital.grant_read_ehr(hospital.public_key, vnode.attrs.client_key)
//                        }
//                    }, 'Grant Read EHR Access'),
//                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            Hospital.revoke_read_ehr(hospital.public_key, vnode.attrs.client_key)
//                        }
//                    }, 'Revoke Read EHR Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.grant_data_processing(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant Data Processing Permission'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.revoke_data_processing(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke Data Processing Permission'),
//                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            Hospital.grant_3rd_party_access(hospital.public_key, vnode.attrs.client_key)
//                        }
//                    }, 'Grant 3rd Party Access'),
//                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            Hospital.revoke_3rd_party_access(hospital.public_key, vnode.attrs.client_key)
//                        }
//                    }, 'Revoke 3rd Party Access'),
//                    m("div"),
//                    m("label.label", "Inclusion/Exclusion criteria"),
//                    m("input.input[type=text][placeholder=Example: excl_height_less=2]", {
//                        oninput: m.withAttr("value", function(value) {Hospital.current.incl_excl_criteria = value}),
//                        value: Hospital.current.incl_excl_criteria
//                    }),
//                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            Hospital.screening_data(hospital.public_key, vnode.attrs.client_key, Hospital.current.incl_excl_criteria)
//                        }
//                    }, 'Get Pre-Screening Data (incl. excl. criteria)'),
//                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            Hospital.get_shared_data(hospital.public_key, vnode.attrs.client_key)
//                        }
//                    }, 'Get Shared Data'),
                    m("div")
                )
            }),
//            m("div"),
//            m(".user-list", Hospital.sharedDataList.map(function(sharedData) {
//                return m("a.user-list-item", "ID: " + sharedData.id
//                    + "; HEIGHT: " + sharedData.height
//                    + "; WEIGHT: " + sharedData.weight
//                    + "; A1C: " + sharedData.A1C
//                    + "; FPG: " + sharedData.FPG
//                    + "; OGTT: " + sharedData.OGTT
//                    + "; RPGT: " + sharedData.RPGT
//                    + "; EVENT_TIME: " + sharedData.event_time)
//            })),
//            m("div"),
//            m("button", {
//                onclick: function() {
//                    Investigator.import_screening_data(Hospital.sharedDataList, vnode.attrs.client_key)
//                }
//            }, 'Import Screening Data'),
=======
                    m("div"),
                    m("button", {
                        onclick: function() {
                            qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + hospital.public_key + '&chld=H|0'
                        }
                    }, 'Generate QR code for Hospital Public Key: ' + hospital.public_key),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.grant_read_ehr(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant Read EHR Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.revoke_read_ehr(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke Read EHR Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.grant_write_ehr(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant Write EHR Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.revoke_write_ehr(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke Write EHR Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.grant_3rd_party_access(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant 3rd Party Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.revoke_3rd_party_access(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke 3rd Party Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Hospital.get_shared_data(hospital.public_key, vnode.attrs.client_key)
                        }
                    }, 'Get Shared Data')
                )
            }),
            m("div"),
            m(".user-list", Hospital.sharedDataList.map(function(sharedData) {
                return m("a.user-list-item", "ID: " + sharedData.id
                    + "; FIELD_1: " + sharedData.field_1
                    + "; FIELD_2: " + sharedData.field_2
                    + "; EVENT_TIME: " + sharedData.event_time)
            })),
>>>>>>> upstream/master
            m("div"),
            m("img", {src: qrcodeurl}),
            m("label.error", Hospital.error))
    }
}
//application root 
define(["backbone", "marionette", "utils/reqcmd", "config/base/auth",'homepage/homepage_app','diagnose/diagnose_app','register/register_app','doctorhome/doctor_home_app','patienthome/patient_home_app'], function(Backbone, Marionette, ReqCmd, Auth, HomePageApp,DiagnoseApp,RegisterApp,DoctorHomeApp,PatientHomeApp) {
		"use strict";
		var App = new Marionette.Application();
		App.addRegions({
			headerRegion: "#header-region",
			mainRegion: "#main-region",
			footerRegion: "#footer-region"
		});

		ReqCmd.reqres.setHandler("default:region", function() {
			// body...
			return App.mainRegion;
		});
		App.Auth = Auth;


		App.addInitializer(function() {
			// body...
			//AdminApp.API.show();
			var location = window.location.pathname;
			console.log(location);
			//use hash to speed up
			if (location.indexOf("homepage") != -1) {
				HomePageApp.API.show();
			} else if(location.indexOf("applyDiagnose") != -1){
				DiagnoseApp.API.applyDiagnose();
			} else if(location.indexOf("register/patient") != -1){
				RegisterApp.API.registerPatient();
			} else if(location.indexOf("register/doctor") != -1){
				RegisterApp.API.registerDoctor();
			} else if(location.indexOf("doctor") != -1){
				DoctorHomeApp.API.show();
			} else if(location.indexOf("patienthome") != -1){
				PatientHomeApp.API.show();
			} else {
				console.log("do not init");
			}
			console.log("App init");

		});
		ReqCmd.commands.setHandler("register:instance", function(instance, id) {
			// body...
			App.register(instance, id);
		});
		ReqCmd.commands.setHandler("unregister:instance", function(instance, id) {
			// body...
			App.unregister(instance, id);
		});
		App.on("initialize:after", function(options) {
			// body...
			console.log("app init after");
		})


		return App;
	}

);
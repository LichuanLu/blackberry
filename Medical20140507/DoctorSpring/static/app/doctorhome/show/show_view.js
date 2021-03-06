define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap", 'bootstrap.select', 'bootstrap-treeview'], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var DoctorHomePageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init DoctorHomePageLayoutView");
			this.bindUIElements();
		},
		regions: {
			"contentRegion": "#contentRegion",
			"newDiagnoseRegion": "#newDiagnoseRegion"
		},
		el: "#doctorhome-content",
		ui: {
			"doctorActionLinks": "#doctor-actions ul a",
			"headerTitle":"#doctor-action-header h6"

		},
		events: {
			"click @ui.doctorActionLinks": "doctorActionLinksHandler"
		},
		attachEndHandler: function() {

			this.ui.doctorActionLinks.filter("[name*='diagnoseLink']").click();
		},
		doctorActionLinksHandler: function(e) {
			e.preventDefault();
			//e.stopPropagation();
			//console.dir($(e.target));
			var $target = $(e.target);
			if ($target.is('span')) {
				$target = $target.closest('a');
			}
			console.log($target.attr("name"));
			this.ui.doctorActionLinks.removeClass('active');
			$target.addClass('active');
			ReqCmd.commands.execute("doctorHomePageLayoutView:changeContentView", $target.attr("name"));

			//change title
			var iconClass = $target.attr('class');
			var titleText = $target.find('.nav-text').html();
			//console.log(iconClass+','+text);
			//console.dir(this.ui);
			this.ui.headerTitle.html("<i class='"+iconClass+"'></i><span>"+titleText+"</span>");

		}

	});

	var DiagnoseListView = Marionette.CompositeView.extend({
		initialize: function() {
			console.log("init DiagnoseTableCollectionView");
		},
		onShow: function() {
			$("select").selectpicker({
				style: 'btn-sm btn-primary'
			});

		},
		ui: {
			"submitBtn": "#doctor-action-content .submit-btn",
			"typeSelect": "#doctor-action-content select"
		},
		events: {
			"click @ui.submitBtn": "searchDiagnose"
		},
		template: "doctorDiagnoseLayout",
		itemViewContainer: "#diagnose-tbody",
		searchDiagnose: function(e) {
			e.preventDefault();
			ReqCmd.commands.execute("DiagnoseListView:searchDiagnose", this.ui.typeSelect.val());
		}

	});

	var DiagnoseTableItemView = Marionette.ItemView.extend({
		initialize: function() {},
		template: "doctorDiagnoseItem",
		ui: {
			"actionLinks": ".action-group a"
		},
		events: {
			"click @ui.actionLinks": "actionHandler"
		},
		onRender: function() {
			//console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);
		},
		actionHandler: function(e) {
			var statusId = this.model.get('statusId');
			if(statusId != 6){
				e.preventDefault();
				ReqCmd.commands.execute("DiagnoseTableItemView:actionHandler",this.model);
			}

		}


	});


	var AccountManageLayoutView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("AccountManageLayoutView init");

		},
		template: "doctorAccountManageLayout",
		ui: {
			"editBtns": ".edit-btn",
			"editBlocks": "#doctor-user-account-form .edit-block"
		},
		events: {
			"click @ui.editBtns": "editFormHandler"
		},
		editFormHandler: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			$target.hide();
			$target.siblings('.edit-block').show();

		},
		onRender: function() {
			this.ui.editBlocks.hide();

		},

		onShow: function() {
			var $this = $(this);
			console.dir($('#accountTab a'));
			$('#accountTab a').click(function(e) {
				e.preventDefault();
				$(this).tab('show');
			});
		}
	});

	var NewDiagnoseLayoutView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init NewDiagnoseLayoutView");
			this.bindUIElements();
		},
		template: "newDiagnoseLayout",
		ui: {
			"loadTemplateBtn": ".load-btn",
			"loadingBtn": ".loading-btn",
			"imageDesTextArea": "#imageDes",
			"diagnoseResultTextArea": "#diagnoseResult",
			"closeLink": ".close-link",
			"submitDiagnoseBtn": '.submit-btn',
			"techDesTextArea":"#techDes"
		},
		events: {
			"click @ui.loadTemplateBtn": "loadTemplate",
			"click @ui.closeLink": "closeRegion",
			"click @ui.submitDiagnoseBtn": "submitDiagnose"
		},
		editFormHandler: function(e) {

		},
		submitDiagnose: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			var targetId = $target.attr("id");
			//console.log(targetId);
			var type;
			if(targetId === 'saveDiagnoseBtn'){
				type = 0;
			}else if(targetId === 'previewDiagnoseBtn'){
				type = 1;
			}else if(targetId === 'submitDiagnoseBtn'){
				type = 2;
			}
			if(type !== 'undefined'){
				var data = $('#new-diagnose-form').serialize()+"&type="+type+"&diagnoseId="+this.model.get('id');
				$.ajax({
					url: '/doctor/diagnose/create',
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.code != 0) {
							this.onError(data);

						} else {
							Messenger().post({
								message: 'SUCCESS. Product import started. Check back periodically.',
								type: 'success',
								showCloseButton: true
							});
						}
					},
					onError: function(res) {
						this.resetForm();
						//var error = jQuery.parseJSON(data);
						if (typeof res.message !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.message,
								type: 'error',
								showCloseButton: true
							});
						}

					}
				});

			}
			

		},
		onRender: function() {

		},
		closeRegion: function(e) {
			e.preventDefault();
			ReqCmd.reqres.request("NewDiagnoseLayoutView:closeRegion");
		},
		loadTemplate: function(e) {
			e.preventDefault();
			var $templateLink = $('#tree ul').find('.node-selected').children('a');
			var href = $templateLink.attr('href');

			console.log(href);
			var that = this;
			if (href !== '#') {
				this.ui.loadTemplateBtn.hide();
				this.ui.loadingBtn.show();
				var data = 'templateId=' + href;
				$.ajax({
					url: '/diagnose/template',
					data: data,
					dataType: 'json',
					type: 'GET',
					success: function(data) {
						if (data.code != 0) {
							this.onError(data);

						} else {
							Messenger().post({
								message: 'SUCCESS. Product import started. Check back periodically.',
								type: 'success',
								showCloseButton: true
							});
							this.setTemplate(data.data);

						}
					},
					onError: function(res) {
						this.resetForm();
						//var error = jQuery.parseJSON(data);
						if (typeof res.message !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.message,
								type: 'error',
								showCloseButton: true
							});
						}

					},
					setTemplate: function(data) {
						if (data) {
							that.ui.imageDesTextArea.val(data.imageDes);
							that.ui.diagnoseResultTextArea.val(data.diagnoseResult);
							that.ui.techDesTextArea.val(data.techDes);
							this.resetForm();
						}

					},
					resetForm: function() {
						that.ui.loadTemplateBtn.show();
						that.ui.loadingBtn.hide();
					}
				});

			}

		},
		onShow: function() {
			console.log(this.ui.templateLinks);
			var data = [{
				text: "X线",
				nodes: [{
					text: "呼吸系统",
					nodes: [{
						text: "心肺未见异常",
						href: "#1"
					}, {
						text: "右肺上叶干酪性肺炎并右肺下叶播放",
						href: "#2"

					}]
				}, {
					text: "骨关节病变",
					nodes: [{
						text: "心肺未见异常",
						href: "#3"
					}, {
						text: "右肺上叶干酪性肺炎并右肺下叶播放",
						href: "#4"
					}]
				}]
			}, {
				text: "CT",
				nodes: [{
					text: "呼吸系统",
					nodes: [{
						text: "心肺未见异常"
					}, {
						text: "右肺上叶干酪性肺炎并右肺下叶播放"

					}]
				}, {
					text: "骨关节病变",
					nodes: [{
						text: "心肺未见异常"
					}, {
						text: "右肺上叶干酪性肺炎并右肺下叶播放"
					}]
				}]
			}, {
				text: "MR",
				nodes: [{
					text: "呼吸系统",
					nodes: [{
						text: "心肺未见异常"
					}, {
						text: "右肺上叶干酪性肺炎并右肺下叶播放"

					}]
				}, {
					text: "骨关节病变",
					nodes: [{
						text: "心肺未见异常"
					}, {
						text: "右肺上叶干酪性肺炎并右肺下叶播放"
					}]
				}]
			}];

			$('#tree').treeview({
				data: data,
				enableLinks: true
				// showBorder:false
			});
		}
	});

	var NewAuditLayoutView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init NewAuditLayoutView");
			this.listenTo(this.model, 'sync', this.render, this);

		},
		template: "newAuditLayout",
		ui: {

			"auditTextArea": "#auditText",
			"closeLink": ".close-link",
			"submitAuditBtn": '.submit-btn'
		},
		events: {
			"click @ui.closeLink": "closeRegion",
			"click @ui.submitAuditBtn": "submitAudit"
		},
		editFormHandler: function(e) {
		},
		submitAudit: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			var targetId = $target.attr("id");
			//console.log(targetId);
			var type;
			if(targetId === 'saveAuditBtn'){
				type = 0;
			}else if(targetId === 'previewAuditBtn'){
				type = 1;
			}else if(targetId === 'submitAuditBtn'){
				type = 2;
			}
			if(type !== 'undefined'){
				var data = $('#new-audit-form').serialize()+"&type="+type+"&diagnoseId="+this.model.get('id');
				$.ajax({
					url: '/doctor/audit/create',
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.code != 0) {
							this.onError(data);

						} else {
							Messenger().post({
								message: 'SUCCESS. Product import started. Check back periodically.',
								type: 'success',
								showCloseButton: true
							});
						}
					},
					onError: function(res) {
						this.resetForm();
						//var error = jQuery.parseJSON(data);
						if (typeof res.message !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.message,
								type: 'error',
								showCloseButton: true
							});
						}

					}
				});

			}
			

		},
		closeRegion: function(e) {
			e.preventDefault();
			ReqCmd.reqres.request("NewDiagnoseLayoutView:closeRegion");
		}
	});


	return {
		DoctorHomePageLayoutView: DoctorHomePageLayoutView,
		DiagnoseListView: DiagnoseListView,
		DiagnoseTableItemView: DiagnoseTableItemView,
		AccountManageLayoutView: AccountManageLayoutView,
		NewDiagnoseLayoutView: NewDiagnoseLayoutView,
		NewAuditLayoutView:NewAuditLayoutView
	}
});
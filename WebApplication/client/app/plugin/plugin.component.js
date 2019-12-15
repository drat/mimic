"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = require("@angular/core");
var index_1 = require("../_services/index");
var index_2 = require("../_services/index");
var PluginComponent = /** @class */ (function () {
    function PluginComponent(userService, script) {
        this.userService = userService;
        this.script = script;
        this.users = [];
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    }
    PluginComponent.prototype.refreshIframe = function () {
        var ifr = document.getElementsByName('Right')[0];
        //ifr.src = ifr.src;
    };
    PluginComponent.prototype.ngOnInit = function () {
        this.loadAllUsers();
    };
    PluginComponent.prototype.loadAllUsers = function () {
        var _this = this;
        this.userService.getAll().subscribe(function (users) { _this.users = users; });
    };
    PluginComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            templateUrl: 'plugin.component.html'
        }),
        __metadata("design:paramtypes", [index_1.UserService, index_2.ScriptService])
    ], PluginComponent);
    return PluginComponent;
}());
exports.PluginComponent = PluginComponent;
//# sourceMappingURL=plugin.component.js.map
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
var http_1 = require("@angular/common/http");
var app_config_1 = require("../app.config");
var UserService = /** @class */ (function () {
    function UserService(http) {
        this.http = http;
    }
    UserService.prototype.getAll = function () {
        return this.http.get(app_config_1.appConfig.apiUrl + '/users');
    };
    UserService.prototype.getById = function (_id) {
        return this.http.get(app_config_1.appConfig.apiUrl + '/users/' + _id);
    };
    UserService.prototype.create = function (user) {
        return this.http.post(app_config_1.appConfig.apiUrl + '/users/register', user);
    };
    UserService.prototype.update = function (user) {
        return this.http.put(app_config_1.appConfig.apiUrl + '/users/' + user._id, user);
    };
    UserService.prototype.delete = function (_id) {
        return this.http.delete(app_config_1.appConfig.apiUrl + '/users/' + _id);
    };
    UserService = __decorate([
        core_1.Injectable(),
        __metadata("design:paramtypes", [http_1.HttpClient])
    ], UserService);
    return UserService;
}());
exports.UserService = UserService;
//# sourceMappingURL=user.service.js.map
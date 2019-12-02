"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var router_1 = require("@angular/router");
var index_1 = require("./home/index");
var index_2 = require("./plugin/index");
var index_3 = require("./login/index");
var index_4 = require("./register/index");
var index_5 = require("./_guards/index");
var appRoutes = [
    { path: '', component: index_2.PluginComponent, canActivate: [index_5.AuthGuard] },
    { path: 'home', component: index_1.HomeComponent, canActivate: [index_5.AuthGuard] },
    { path: 'login', component: index_3.LoginComponent },
    { path: 'register', component: index_4.RegisterComponent },
    // otherwise redirect to home
    { path: '**', redirectTo: '' }
];
exports.routing = router_1.RouterModule.forRoot(appRoutes);
//# sourceMappingURL=app.routing.js.map
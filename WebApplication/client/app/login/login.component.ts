import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { AlertService, AuthenticationService } from '../_services/index';
// Now, within any of the app files (ES2015 style)
declare var $: any;


@Component({
    moduleId: module.id,
    templateUrl: 'login.component.html'
})

export class LoginComponent implements OnInit {
    model: any = {};
    loading = false;
    returnUrl: string;

    constructor( private route: ActivatedRoute, private router: Router, private authenticationService: AuthenticationService, private alertService: AlertService) { }

    myHandler() {
        $("#myVideo").fadeOut(1000);
        $("#loginForm").fadeIn(3000);
    }
    ngOnInit() {
        setTimeout(() => this.myHandler(), 3000);

        // reset login status
        this.authenticationService.logout();

        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';

    }
    login() {
        this.loading = true;
        this.authenticationService.login(this.model.username, this.model.password)
            .subscribe(
                data => {
                    this.router.navigate([this.returnUrl]);
                },
                error => {
                    this.alertService.error(error);
                    this.loading = false;
                });
    }
}

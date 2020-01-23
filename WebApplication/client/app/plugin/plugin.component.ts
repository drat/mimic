import { Component, OnInit } from '@angular/core';
import { User } from '../_models/index';
import { UserService } from '../_services/index';
import { ScriptService } from '../_services/index';


declare var $: any;

@Component({
    moduleId: module.id,
    templateUrl: 'plugin.component.html'
})

export class PluginComponent implements OnInit {
    currentUser: User;
    users: User[] = [];
    constructor(private userService: UserService, private script: ScriptService) {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    }

    refreshIframe() {
        var ifr = document.getElementsByName('Right')[0];
        //ifr.src = ifr.src;
    }
    ngOnInit(){
        this.loadAllUsers();
    }
    private loadAllUsers(){
        this.userService.getAll().subscribe(users => { this.users = users; });
    }

}
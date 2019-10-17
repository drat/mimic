import { Component, OnInit } from '@angular/core';
import { User } from '../_models/index';
import { UserService } from '../_services/index';
import { ScriptService } from '../_services/index';
import * as $ from "jquery";

@Component({
    moduleId: module.id,
    templateUrl: 'plugin.component.html'
})

export class PluginComponent implements OnInit {
    currentUser: User;
    users: User[] = [];

    constructor(private userService: UserService, private script: ScriptService) {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
        /* Load external Scripts, method other then placement in index.html

        this.script.load('janus', 'frames').then(data => {console.log('script loaded ', data);}).catch(error => console.log("ERROR FROM LOADER", error));

        */
    }

    ngOnInit(){
        this.loadAllUsers();
    }

    private loadAllUsers(){
        this.userService.getAll().subscribe(users => { this.users = users; });
    }

}
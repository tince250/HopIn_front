import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PassengerAccountOptionsService } from '../services/passengerAccountOptions.service';
import { UserService } from '../services/user.service';
 
@Component({
  selector: 'app-account-options',
  templateUrl: './account-options.component.html',
  styleUrls: ['./account-options.component.css']
})
export class AccountOptionsComponent implements OnInit {

  constructor(private router: Router, 
    private userService: UserService,
    private passengerAccountOptionsService : PassengerAccountOptionsService) { }

  option : string = "documents";
  role: string = "passenger";

  ngOnInit(): void {
    this.selectOption(this.option);
    this.role = this.userService.role;
  }

  selectOption(option: string){
    this.option = option;
    this.sendSelectedOption(option);
  }

  sendSelectedOption(option: string): void {
    this.passengerAccountOptionsService.sendSelectedOption(option);
  }
}

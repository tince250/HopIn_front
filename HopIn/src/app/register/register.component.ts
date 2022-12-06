import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { passwordMatcher } from '../validators/passwordMatch';
import { ConfirmValidParentMatcher } from '../validators/passwordMatch';

@Component({
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  confirmValidParentMatcher = new ConfirmValidParentMatcher();

  registerForm = new FormGroup({
    name: new FormControl('', [Validators.required]),
    surname: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required]),
    confpass: new FormControl('', [Validators.required]),
    city: new FormControl('', [Validators.required]),
    phonenum: new FormControl('', [Validators.required]),
  }, [passwordMatcher("password", "confpass")])

  constructor() { }

  ngOnInit(): void {
  }

  register() {
    if (this.registerForm.valid) {
      alert("registration successful, email confirmation needed.");
    }
  }

}

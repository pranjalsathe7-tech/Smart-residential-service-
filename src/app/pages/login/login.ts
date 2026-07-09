import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent {

  email: string = '';
  password: string = '';
  role: string = 'user';

  constructor(private router: Router) {}

  login() {
    // Simple validation
    if (!this.email || !this.password) {
      alert('Please fill all fields');
      return;
    }

    // Demo login logic (replace with backend later)
    if (this.role === 'admin') {
      this.router.navigate(['/admin']);
    } else if (this.role === 'worker') {
      this.router.navigate(['/worker']);
    } else {
      this.router.navigate(['/']);
    }

    console.log('Login Data:', {
      email: this.email,
      password: this.password,
      role: this.role
    });
  }

  goToSignup() {
    this.router.navigate(['/registration']);
  }
}
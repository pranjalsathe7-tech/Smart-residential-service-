import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

  // Property (data)
  title: string = "Welcome to Home Page";

  // Inject Router for navigation
  constructor(private router: Router) {}

  // Method: Show alert
  showMessage() {
    alert("Hello! This is Home Component 🚀");
  }

  // Method: Navigate to another page
  goToServices() {
    this.router.navigate(['/services']);
  }

  // Method: Dynamic greeting
  getGreeting() {
    return "Have a great day! 😊";
  }
}
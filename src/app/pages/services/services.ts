import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-services',
  templateUrl: './services.html',
  styleUrls: ['./services.css']
})
export class ServicesComponent {

  constructor(private router: Router) {}

  services = [
    {
      name: 'Plumbing',
      desc: 'Plumbing services including repairs and installations',
      image: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952'
    },
    {
      name: 'Electrical',
      desc: 'Electrical services including repairs and installations',
      image: 'https://images.unsplash.com/photo-1581090700227-1e8a1caa4c3b'
    },
    {
      name: 'Cleaning',
      desc: 'Home cleaning services',
      image: 'https://images.unsplash.com/photo-1581579186986-d6f2b47b51a0'
    }
  ];

  // Navigate to available page
  bookService(service: any) {
    this.router.navigate(['/available'], {
      queryParams: { service: service.name }
    });
  }
}
import { Component } from '@angular/core';

@Component({
  selector: 'app-availbal',
  templateUrl: './availbal.html',
  styleUrls: ['./availbal.css']
})
export class Availbal {

  // Sample data (you can replace with API later)
  services = [
    { id: 1, name: 'Plumbing', available: true },
    { id: 2, name: 'Electrician', available: false },
    { id: 3, name: 'Cleaning', available: true }
  ];

  // Toggle availability
  toggleAvailability(service: any) {
    service.available = !service.available;
  }

  // Add new service
  addService(name: string) {
    if (name.trim() !== '') {
      this.services.push({
        id: this.services.length + 1,
        name: name,
        available: true
      });
    }
  }

  // Delete service
  deleteService(id: number) {
    this.services = this.services.filter(s => s.id !== id);
  }
}
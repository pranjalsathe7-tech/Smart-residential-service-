import { Component } from '@angular/core';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.html',
  styleUrls: ['./admin.css']
})
export class AdminComponent {

  // Sample data (replace with API later)
  users = [
    { id: 1, name: 'User1' },
    { id: 2, name: 'User2' },
    { id: 3, name: 'User3' },
    { id: 4, name: 'User4' },
    { id: 5, name: 'User5' },
    { id: 6, name: 'User6' },
    { id: 7, name: 'User7' }
  ];

  workers = [
    { id: 1, name: 'Worker1' },
    { id: 2, name: 'Worker2' },
    { id: 3, name: 'Worker3' },
    { id: 4, name: 'Worker4' }
  ];

  categories = [
    'Plumbing',
    'Electrical',
    'Cleaning',
    'Painting',
    'Carpentry',
    'AC Repair',
    'Computer'
  ];

  services = [
    'Fan Repair',
    'PC Repair',
    'Mixer Repair',
    'Plumbing Service'
  ];

  // Dynamic getters
  get totalUsers() {
    return this.users.length;
  }

  get totalWorkers() {
    return this.workers.length;
  }

  get totalCategories() {
    return this.categories.length;
  }

  get totalServices() {
    return this.services.length;
  }
}
import { Component } from '@angular/core';

@Component({
  selector: 'app-service',
  templateUrl: './service.html',
  styleUrls: ['./service.css']
})
export class ServiceComponent {

  services = [
    { id: 1, name: 'Fan Repair', category: 'Electrical', desc: 'Fan repair service available', price: 100, date: '2025-05-01' },
    { id: 2, name: 'PC Repair', category: 'Computer', desc: 'PC repair service', price: 100, date: '2025-05-02' },
    { id: 3, name: 'Mixer Repair', category: 'Electrical', desc: 'Mixer repair service', price: 100, date: '2025-05-02' },
    { id: 4, name: 'Plumbing Service', category: 'Plumbing', desc: 'Home plumbing service', price: 100, date: '2025-05-02' }
  ];

  // Add new service
  addService() {
    const newService = {
      id: this.services.length + 1,
      name: 'New Service',
      category: 'General',
      desc: 'New service description',
      price: 0,
      date: new Date().toISOString().split('T')[0]
    };
    this.services.push(newService);
  }

  // Delete service
  deleteService(id: number) {
    this.services = this.services.filter(s => s.id !== id);
  }

  // Edit service (simple example)
  editService(service: any) {
    service.name = prompt('Enter new name', service.name) || service.name;
    service.price = prompt('Enter new price', service.price) || service.price;
  }
}
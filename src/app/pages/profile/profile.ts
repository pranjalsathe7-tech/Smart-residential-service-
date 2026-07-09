import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.html',
  styleUrls: ['./profile.css']
})
export class ProfileComponent implements OnInit {

  user: any = {
    name: '',
    role: '',
    email: '',
    phone: '',
    address: ''
  };

  isEdit: boolean = false;

  // Dummy request data
  requests = [
    { status: 'completed' },
    { status: 'pending' },
    { status: 'cancelled' }
  ];

  ngOnInit() {
    // Load user from localStorage
    const data = localStorage.getItem('user');

    if (data) {
      const parsed = JSON.parse(data);

      this.user = {
        name: parsed.email.split('@')[0],
        role: parsed.role,
        email: parsed.email,
        phone: parsed.phone || 'Not set',
        address: parsed.address || 'Not set'
      };
    }
  }

  // Toggle edit mode
  toggleEdit() {
    this.isEdit = !this.isEdit;
  }

  // Save profile
  saveProfile() {
    localStorage.setItem('user', JSON.stringify(this.user));
    this.isEdit = false;
    alert('Profile updated successfully!');
  }

  // Summary counts
  get totalRequests() {
    return this.requests.length;
  }

  get completed() {
    return this.requests.filter(r => r.status === 'completed').length;
  }

  get pending() {
    return this.requests.filter(r => r.status === 'pending').length;
  }

  get cancelled() {
    return this.requests.filter(r => r.status === 'cancelled').length;
  }
}
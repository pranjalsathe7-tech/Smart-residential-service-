import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-registation',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './registation.html',
  styleUrl: './registation.css',
})
export class Registation {

  // Form Fields
  user = {
    username: 'sakshi',
    email: 'sakshispawar200@ gmail.com',
    password: '123456'
  };

  // Submit Function
  onSubmit(form: any) {
    if (form.valid) {
      console.log('Form Data:', this.user);

      alert('Registration Successful!');

      // Reset form
      form.reset();
    } else {
      alert('Please fill all fields correctly!');
    }
  }
}
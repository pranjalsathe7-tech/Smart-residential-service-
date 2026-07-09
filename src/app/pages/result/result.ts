import { Component } from '@angular/core';

@Component({
  selector: 'app-result',
  templateUrl: './result.html',
  styleUrls: ['./result.css']
})
export class Result {

  subjects = [
    { name: 'Math', marks: 80 },
    { name: 'Science', marks: 70 },
    { name: 'English', marks: 85 }
  ];

  // Calculate total marks
  getTotal(): number {
    return this.subjects.reduce((sum, sub) => sum + sub.marks, 0);
  }

  // Calculate percentage
  getPercentage(): number {
    return this.getTotal() / this.subjects.length;
  }

  // Check pass/fail
  getResult(): string {
    return this.getPercentage() >= 35 ? 'Pass' : 'Fail';
  }

  // Add new subject
  addSubject(name: string, marks: number) {
    if (name && marks >= 0) {
      this.subjects.push({ name, marks });
    }
  }

  // Delete subject
  deleteSubject(index: number) {
    this.subjects.splice(index, 1);
  }
}
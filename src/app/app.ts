import { HttpClient } from '@angular/common/http';
import { Component, Signal, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Login } from "./pages/login/login";
import { Registation } from "./pages/registation/registation";
import { Result } from './pages/result/result';
import { Home } from './pages/home/home';

@Component({
  selector: 'app-root',
  imports: [FormsModule, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  @ViewChild('myRef') form: any;


  url = "http://127.0.0.1:8000/add"

  username = ""
  email = ""
  password = ""


  constructor(public http: HttpClient) { }


  dataSubmit(data: any) {

    console.log("form Submit")
    console.log(this.form)
    let jsonObj = {

      "username": this.username,
      "email": this.email,
      "password": this.password
    }

    console.log(jsonObj);

    this.http.post(this.url, jsonObj).subscribe({
      next: (res: any) => {

        console.log(res);


      }
    })
  }



}

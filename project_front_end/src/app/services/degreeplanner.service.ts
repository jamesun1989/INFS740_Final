import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DegreeplannerService {
  //api_url:string = 'http://localhost:5000/api/students';
  api_url:string = 'http://127.0.0.1:5000';
  headers = new HttpHeaders().set('Content-Type', 'application/json');

  constructor(private http: HttpClient) { }

  createStudyPlan(data): Observable<any> {
    let base_url = `${this.api_url}/create`;
    return this.http.post(base_url, data);
  }

  getStudyPlan() {
    let base_url = `${this.api_url}/getallSP`;
    return this.http.get(base_url);
  }
}

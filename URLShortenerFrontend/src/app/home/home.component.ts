import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environments/environment';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {

    constructor(
        private http: HttpClient) {

    }

    long_url: string = "";
    short_url: string = "";
    history_list: any;

    generate_result(){
        // return this.http.post(`${environment.apiUrl}/api/v1/urlshortener/urlshorten`, {})
        // .pipe(map(user => {
        //     // store user details and jwt token in local storage to keep user logged in between page refreshes
        //     localStorage.setItem('user', JSON.stringify(user));
        //     this.userSubject.next(user);
        //     return user;
        // }));
        this.http.post<any>(`${environment.apiUrl}/api/v1/urlshortener/urlshorten`,
                             { long_url: this.long_url }, {withCredentials:true}).subscribe(data => {
            this.short_url = data.short_url
        })
    }

    generate_history(){
        this.http.get<any>(`${environment.apiUrl}/api/v1/urlshortener/urlshorten`,
                            {withCredentials:true}).subscribe(data => {
            console.log(data);
            this.history_list = data
        })
    }

}
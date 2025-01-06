import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Observable, of } from 'rxjs';
import { delay, catchError } from 'rxjs/operators';

interface Machine {
  id: number;
  name: string;
  price: number;
  description: string;
  category: string;
}

@Component({
  selector: 'app-trailers',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './trailers.component.html',
  styleUrls: ['./trailers.component.css']
})
export class TrailersComponent implements OnInit {
  machines: Machine[] = [];
  status: string = 'Ładowanie...';
  noMachinesMessage$: Observable<string> | undefined;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<Machine[]>('http://localhost:5000/rental/trailers').pipe(
      catchError(() => {
        this.status = 'Błąd podczas ładowania danych';
        return of([]);
      })
    ).subscribe(
      (data) => {
        console.log('Otrzymane dane:', data);
        this.machines = data;
        this.status = `Załadowano ${this.machines.length} przyczep`;
        if (this.machines.length === 0) {
          this.noMachinesMessage$ = of('Brak dostępnych przyczep').pipe(delay(2000));
        }
      }
    );
  }
}

import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule, NgOptimizedImage } from '@angular/common';

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
  imports: [CommonModule, HttpClientModule, NgOptimizedImage],
  templateUrl: './trailers.component.html',
  styleUrls: ['./trailers.component.css']
})
export class TrailersComponent implements OnInit {
  machines: Machine[] = [];
  status: string = 'Ładowanie...';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<Machine[]>('http://localhost:5000/rental/trailers').subscribe(
      (data) => {
        console.log('Otrzymane dane:', data);
        this.machines = data;
        this.status = `Załadowano ${this.machines.length} przyczep`;
      },
      (error) => {
        console.error('Błąd podczas pobierania danych:', error);
        this.status = 'Błąd podczas ładowania danych';
      }
    );
  }
}

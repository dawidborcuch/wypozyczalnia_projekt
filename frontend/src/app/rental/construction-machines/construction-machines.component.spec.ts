import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

interface Machine {
  id: number;
  name: string;
  price: number;
  description: string;
  category: string;
}

@Component({
  selector: 'app-construction-machines',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Maszyny budowlane</h2>
    <ul>
      <li *ngFor="let machine of machines">
        <h3>{{ machine.name }}</h3>
        <p><strong>Cena:</strong> {{ machine.price | currency:'PLN':'symbol':'1.2-2' }} / dzień</p>
        <p>{{ machine.description }}</p>
      </li>
    </ul>
  `,
  styles: [`
    ul {
      list-style-type: none;
      padding: 0;
    }
    li {
      border: 1px solid #ddd;
      margin-bottom: 10px;
      padding: 15px;
      border-radius: 5px;
    }
    h3 {
      margin-top: 0;
      color: #333;
    }
    p {
      margin: 5px 0;
    }
  `]
})
export class ConstructionMachinesComponent implements OnInit {
  machines: Machine[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<Machine[]>('http://localhost:5000/rental/construction').subscribe(
      (data) => {
        this.machines = data;
      },
      (error) => {
        console.error('Błąd podczas pobierania danych:', error);
      }
    );
  }
}

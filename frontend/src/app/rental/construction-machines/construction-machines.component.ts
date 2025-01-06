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
  selector: 'app-construction-machines',
  standalone: true,
  imports: [CommonModule, HttpClientModule, NgOptimizedImage],
  template: `
    <h2>Maszyny budowlane</h2>
    <div *ngIf="machines.length > 0; else noMachines">
      <ul>
        <li *ngFor="let machine of machines">
          <h3>{{ machine.name }}</h3>
          <p><strong>Cena:</strong> {{ machine.price | currency:'PLN':'symbol':'1.2-2' }} / dzień</p>
          <p>{{ machine.description }}</p>
        </li>
      </ul>
    </div>
    <ng-template #noMachines>
      <p>Brak dostępnych maszyn budowlanych.</p>
    </ng-template>
    <p>Status: {{ status }}</p>
  `,
  styleUrls: ['./construction-machines.component.css']
})
export class ConstructionMachinesComponent implements OnInit {
  machines: Machine[] = [];
  status: string = 'Ładowanie...';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<Machine[]>('http://localhost:5000/rental/construction').subscribe(
      (data) => {
        console.log('Otrzymane dane:', data);
        this.machines = data;
        this.status = `Załadowano ${this.machines.length} maszyn`;
      },
      (error) => {
        console.error('Błąd podczas pobierania danych:', error);
        this.status = 'Błąd podczas ładowania danych';
      }
    );
  }

}

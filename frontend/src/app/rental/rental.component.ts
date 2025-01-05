import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NgOptimizedImage } from '@angular/common';

interface Machine {
  id: number;
  name: string;
  price: number;
  description: string;
}

@Component({
  selector: 'app-rental',
  standalone: true,
  imports: [CommonModule, HttpClientModule, NgOptimizedImage],
  templateUrl: './rental.component.html',
  styleUrls: ['./rental.component.css']
})
export class RentalComponent implements OnInit {
  machines: Machine[] = [];
  imageUrl: string = 'assets/images/1.png'; // Dodaj tę linię

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<Machine[]>('http://localhost:5000/rental').subscribe(
      (data) => {
        this.machines = data;
      },
      (error) => {
        console.error('Błąd podczas pobierania danych:', error);
      }
    );
  }
}

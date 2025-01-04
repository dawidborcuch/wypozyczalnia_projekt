import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface WeatherData {
  date: string;
  sunrise: string;
  sunset: string;
  day: {
    temp_max: string;
    temp_min: string;
    felt_temp_max: string;
    felt_temp_min: string;
    humidity: string;
    pressure: string;
    wind_speed: string;
    wind_direction: string;
  };
  night: {
    temp_max: string;
    temp_min: string;
    felt_temp_max: string;
    felt_temp_min: string;
    snow_precipitation: string;
    wind_speed: string;
    wind_direction: string;
  };
}

@Component({
  selector: 'app-main-site',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './main-site.component.html',
  styleUrls: ['./main-site.component.css']
})
export class MainSiteComponent implements OnInit {
  weatherData: WeatherData | null = null;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.http.get<WeatherData>('http://localhost:5000/weather').subscribe(
      (data) => {
        this.weatherData = data;
        console.log(this.weatherData);
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );
  }
}

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SubmitStudyPlanComponent } from './components/submit-studyplan/submit-studyplan.component';
import { StudyPlanListComponent } from './components/studyplan-list/studyplan-list.component';

import { DegreeplannerService } from 'src/app/services/degreeplanner.service';

@NgModule({
  declarations: [
    AppComponent,
    SubmitStudyPlanComponent,
    StudyPlanListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [DegreeplannerService],
  bootstrap: [AppComponent]
})
export class AppModule { }

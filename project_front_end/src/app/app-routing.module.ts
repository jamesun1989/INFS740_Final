import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SubmitStudyPlanComponent } from './components/submit-studyplan/submit-studyplan.component';
import { StudyPlanListComponent } from './components/studyplan-list/studyplan-list.component';

const routes: Routes = [
  { path: '', redirectTo: 'submit', pathMatch: 'full'},
  { path: 'submit', component: SubmitStudyPlanComponent },
  { path: 'list', component: StudyPlanListComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

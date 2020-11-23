import { Component } from '@angular/core';
import { DegreeplannerService } from 'src/app/services/degreeplanner.service';

@Component({
  selector: 'app-studyplan-list',
  templateUrl: './studyplan-list.component.html',
  styleUrls: ['./studyplan-list.component.css']
})
export class StudyPlanListComponent {
  studyPlan: any;

  constructor(private dgService: DegreeplannerService) {
    this.getStudyPlans();
   }

  getStudyPlans(){
    this.dgService.getStudyPlan().subscribe((data) => {
      this.studyPlan = data;
    })
  }

}

import { Component, NgZone } from '@angular/core';
import { DegreeplannerService } from 'src/app/services/degreeplanner.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-studyplan-list',
  templateUrl: './studyplan-list.component.html',
  styleUrls: ['./studyplan-list.component.css']
})
export class StudyPlanListComponent {
  studyPlan: any;
  recommendedList: any;

  constructor(private dgService: DegreeplannerService, private router: Router, private ngZone: NgZone) {
    this.getStudyPlans();
    this.getRecommendList();
   }

  getStudyPlans(){
    this.dgService.getStudyPlan().subscribe((data) => {
      this.studyPlan = data;
    })
  }

  getRecommendList(){
    this.dgService.getRecommendList().subscribe((data) => {
      this.recommendedList = data;
    })
  }

  /*

  deleteAllStudyPlans(){
    this.dgService.deleteAllSP().subscribe((data) => {
      this.getStudyPlans()
    })
  }
  */

  onClick() {
      this.dgService.deleteAllSP().subscribe(
        (res) => {
          console.log("Deleted Successfully!")
          this.ngZone.run(() => this.router.navigateByUrl('/submit'))
        }, (error) => {
          console.log(error);
        }
      );
  }

}

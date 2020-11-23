import { Component, NgZone } from '@angular/core';
import { DegreeplannerService } from 'src/app/services/degreeplanner.service';
import { FormBuilder, FormGroup, FormArray, Validators } from "@angular/forms";
import { Router } from '@angular/router';

@Component({
  selector: 'app-submit-studyplan',
  templateUrl: './submit-studyplan.component.html',
  styleUrls: ['./submit-studyplan.component.css']
})

export class SubmitStudyPlanComponent {

  data = {
    studyPlans: [
      {
        dcode: "",
        cno: "",
        cname: "",
        grade: "",
        area: ""
      }
    ]
  };

  myForm: FormGroup;
  submitted = false;
  area_val:any = ['Theoretical Computer Science', 'Systems and Networks', 'Artificial Intelligence and Databases', 'Programming Languages and Software Engineering', 'Computer Vision']

  constructor(private fb: FormBuilder, private dpService: DegreeplannerService, private router: Router,
    private ngZone: NgZone) {
    this.myForm = this.fb.group({
      name: [""],
      studyPlans: this.fb.array([]),
    });

    this.setStudyPlans();
  }

  updateArea(e){
    this.myForm.controls.studyPlans.get('area').setValue(e, {
      onlySelf: true
    })
  }

  addStudyPlans() {
    let control = <FormArray>this.myForm.controls.studyPlans;
    control.push(
      this.fb.group({
        dcode: [""],
        cno: [""],
        cname: [""],
        grade: [""],
        area: [""]
      })
    );
  }

  deleteStudyPlans(index) {
    let control = <FormArray>this.myForm.controls.studyPlans;
    control.removeAt(index);
  }

  setStudyPlans() {
    let control = <FormArray>this.myForm.controls.studyPlans;
    this.data.studyPlans.forEach(x => {
      control.push(
        this.fb.group({
          dcode: x.dcode,
          cno: x.cno,
          cname: x.cname,
          grade: x.grade,
          area: x.area
        })
      );
    });
  }

  resetForm(){
    this.myForm.reset();
  }

  onSubmit() {
    this.submitted = true;
      this.dpService.createStudyPlan(this.myForm.value).subscribe(
        (res) => {
          console.log("Inserted Successfully!")
          this.ngZone.run(() => this.router.navigateByUrl('/list'))
        }, (error) => {
          console.log(error);
        }
      );
  }
}

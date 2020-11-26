import { Component, NgZone } from '@angular/core';
import { DegreeplannerService } from 'src/app/services/degreeplanner.service';
import { FormBuilder, FormGroup, FormArray, FormControl, Validators } from "@angular/forms";
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

  data_area: Array<any> = [
    { area: 'Theoretical Computer Science', value: 'Theoretical Computer Science'},
    { area: 'Systems and Networks', value: 'Systems and Networks'},
    { area: 'Artificial Intelligence and Databases', value: 'Artificial Intelligence and Databases'},
    { area: 'Programming Languages and Software Engineering', value: 'Programming Languages and Software Engineering'},
    { area: 'Computer Vision', value: 'Computer Vision'}
  ];

  myForm: FormGroup;
  submitted = false;
  area_val:any = ['Theoretical Computer Science', 'Systems and Networks', 'Artificial Intelligence and Databases', 'Programming Languages and Software Engineering', 'Computer Vision']

  constructor(private fb: FormBuilder, private dpService: DegreeplannerService, private router: Router,
    private ngZone: NgZone) {
    this.myForm = this.fb.group({
      name: [""],
      studyPlans: this.fb.array([]),
      interestedArea: this.fb.array([], [Validators.required, Validators.minLength(1), Validators.maxLength(3)]),
      cs530_cond: ["1"],
      cs531_cond: ["1"]
    });

    this.setStudyPlans();
  }

  get rdutton() {
    return this.myForm.get('cs530_cond');
  }

  get rdbutton1() {
    return this.myForm.get('cs531_cond');
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

onCheckboxChange(e) {
  let interestedArea = <FormArray>this.myForm.get('interestedArea');

  if (e.target.checked) {
    interestedArea.push(new FormControl(e.target.value));
  } else {
    let i: number = 0;
    interestedArea.controls.forEach((item: FormControl) => {
      if (item.value == e.target.value) {
        interestedArea.removeAt(i);
        return;
      }
      i++;
    });
  }
}
}

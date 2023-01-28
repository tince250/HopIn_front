import { Router } from '@angular/router';
import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ReviewDTO, RideReviewService } from '../services/ride-review.service';
import { SharedService } from '../shared/shared.service';

@Component({
  selector: 'app-ride-review',
  templateUrl: './ride-review.component.html',
  styleUrls: ['./ride-review.component.css']
})
export class RideReviewComponent implements OnInit {

  current: number = 5;
  reviews: ReviewDTO[] = [];

  constructor(private rideReview: RideReviewService,
    private sharedService: SharedService,
    public dialogRef: MatDialogRef<RideReviewComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private router: Router) { }

  reviewForm = new FormGroup({
    driverReviewComment: new FormControl('', [Validators.required]),
    vehicleReviewComment: new FormControl('', [Validators.required]),
  }, [])

  ngOnInit(): void {
  }

  submit(){
    if (this.reviewForm.valid) {
      this.reviews.push(this.setDriverReviewResponseFromForm());
      this.reviews.push(this.setVehicleReviewResponseFromForm());
      this.submitCompleteReview();
    } else {
        this.sharedService.openInvalidInputSnack();
    }
  }

  private submitCompleteReview() {
    this.rideReview.addCompleteReview(this.reviews, this.data.rideId).subscribe({
      next: (res) => {
        this.sharedService.openSnack({
          value: "You've successfully submitted reviews!",
          color: "back-green"
        }
        );
        this.dialogRef.close();
        this.router.navigate(["order-ride"]);
      },
      error: (error) => {
        this.sharedService.openSnack({
          value: error,
          color: "back-red"
        })
      }
    });
  }

  setVehicleReviewResponseFromForm(): ReviewDTO{
    return {
      rating: 4,
      comment: this.reviewForm.value.vehicleReviewComment!
    }
  }

  setDriverReviewResponseFromForm(): ReviewDTO{
    return {
      rating: 3,
      comment: this.reviewForm.value.driverReviewComment!
    }
  }
}

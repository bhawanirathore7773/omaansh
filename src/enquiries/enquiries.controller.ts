import { Body, Controller, Post, Res } from '@nestjs/common';
import { Response } from 'express';
import { CreateEnquiryDto } from './dto/create-enquiry.dto';
import { EnquiriesService } from './enquiries.service';

@Controller()
export class EnquiriesController {
  constructor(private readonly enquiries: EnquiriesService) {}

  @Post('enquiries')
  async create(@Body() dto: CreateEnquiryDto, @Res() res: Response) {
    await this.enquiries.create(dto);
    return res.redirect(303, '/?enquiry=sent#enquiry');
  }
}

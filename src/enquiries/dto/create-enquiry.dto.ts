import { IsEmail, IsInt, IsOptional, IsString, Length, Matches, MaxLength, Min } from 'class-validator';

export class CreateEnquiryDto {
  @IsString()
  @Length(2, 200)
  name!: string;

  @IsString()
  @Matches(/^[0-9+()\-\s]{7,20}$/)
  phone!: string;

  @IsOptional()
  @IsEmail()
  @MaxLength(254)
  email?: string;

  @IsString()
  @Length(2, 100)
  city!: string;

  @IsString()
  @Length(10, 4000)
  message!: string;

  @IsOptional()
  @IsInt()
  @Min(1)
  productId?: number;

  @IsOptional()
  @IsString()
  @MaxLength(100)
  website?: string;
}

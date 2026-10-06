import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { ProductsModule } from './products/products.module';
import { CategoriesModule } from './categories/categories.module';
import { ServicesModule } from './services/services.module';
import { IndustriesModule } from './industries/industries.module';
import { CitiesModule } from './cities/cities.module';
import { BlogModule } from './blog/blog.module';
import { SiteModule } from './site/site.module';

@Module({
  imports: [PrismaModule, ProductsModule, CategoriesModule, ServicesModule, IndustriesModule, CitiesModule, BlogModule, SiteModule],
})
export class AppModule {}

import { Routes } from '@angular/router';

import { Registation } from './pages/registation/registation';
import { Home } from './pages/home/home';
import { LoginComponent } from './pages/login/login';
import { ProfileComponent } from './pages/profile/profile';
import { Result } from './pages/result/result';
import { Availbal } from './pages/availbal/availbal';
import { ServicesComponent } from './pages/services/services';
import { AdminComponent } from './pages/admin/admin';
import { User } from './pages/user/user';
export const routes: Routes = [
    { path: "", component: Home },
    { path: 'Registration', component: Registation },
    { path: 'login', component: LoginComponent },
    { path: 'result', component: Result },
    { path: 'availbal', component: Availbal },
    { path: 'services', component: ServicesComponent },
    { path: 'user', component: User },
    { path: 'admin', component:AdminComponent },
    { path: 'profile', component: ProfileComponent},
    { path: 'Service ', component: ServicesComponent },
];

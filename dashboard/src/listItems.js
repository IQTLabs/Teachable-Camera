import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import ShoppingCartIcon from '@material-ui/icons/ShoppingCart';
import PeopleIcon from '@material-ui/icons/People';
import BarChartIcon from '@material-ui/icons/BarChart';
import LayersIcon from '@material-ui/icons/Layers';

import AirplanemodeActiveIcon from '@material-ui/icons/AirplanemodeActive';
import BlurLinearIcon from '@material-ui/icons/BlurLinear';
import FastfoodIcon from '@material-ui/icons/Fastfood';
import FlashOnIcon from '@material-ui/icons/FlashOn';
import GolfCourseIcon from '@material-ui/icons/GolfCourse';
import HeadsetMicIcon from '@material-ui/icons/HeadsetMic';
import LocationOnIcon from '@material-ui/icons/LocationOn';

//import  from '@material-ui/icons/Assignment';
import AssignmentIcon from '@material-ui/icons/Book';
export const mainListItems = (
  <div>
    <ListItem button>
      <ListItemIcon>
        <AirplanemodeActiveIcon />
      </ListItemIcon>
      <ListItemText primary="Airborne" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <FastfoodIcon />
      </ListItemIcon>
      <ListItemText primary="Operation Dinner Out" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <FlashOnIcon />
      </ListItemIcon>
      <ListItemText primary="Flash" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <HeadsetMicIcon />
      </ListItemIcon>
      <ListItemText primary="Mike" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <GolfCourseIcon />
      </ListItemIcon>
      <ListItemText primary="Golf" />
    </ListItem>
  </div>
);

export const secondaryListItems = (
  <div>
    <ListSubheader inset>Locations</ListSubheader>
    <ListItem button>
      <ListItemIcon>
        <LocationOnIcon />
      </ListItemIcon>
      <ListItemText primary="Danger Zone" />
    </ListItem>
  </div>
);

import React from 'react';
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Title from './Title';

function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles({
  depositContext: {
    flex: 1,
  },
});

export default function Deposits(props) {
  const classes = useStyles();
  return (
    <React.Fragment>
      <Title>Currently Detected</Title>
      <Typography component="p" variant="h4">
        {props.cars}
      </Typography>
      <Typography color="textSecondary" className={classes.depositContext}>
        Cars
      </Typography>
      <Typography component="p" variant="h4">
        {props.trucks}
      </Typography>
      <Typography color="textSecondary" className={classes.depositContext}>
        Trucks
      </Typography>
      <Typography component="p" variant="h4">
        {props.garbageTrucks}
      </Typography>
      <Typography color="textSecondary" className={classes.depositContext}>
        Garbage Trucks
      </Typography>
    </React.Fragment>
  );
}

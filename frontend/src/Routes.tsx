import React, { FC } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import { useHistory } from 'react-router';

import {
  Home,
  Room,
  RoomProps,
} from './views';
import { NavBar, SideBar } from './components';

export const Routes: FC = () => {
  const history = useHistory();

  return (
    <BrowserRouter>
      <Switch></Switch>
      <div className="wrapper">
        <SideBar />
        <div className="main-panel">
          <NavBar />
          <Route exact path="/" component={Home} />
          <Route path="/room/:name" component={(props: RoomProps) => <Room {...props} /> } />
        </div>
      </div>
    </BrowserRouter>
  );
};

import '../src/index.css';
import '../src/assets/css/fonts.css'

import React from "react";
import { addDecorator } from "@storybook/react";
import { MemoryRouter } from "react-router-dom";
import { store } from '../src/app/store';
import { Provider } from 'react-redux';
import { TimerHandler } from '../src/components/TimerHandler';

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
}

addDecorator(story => <TimerHandler>{story()}</TimerHandler>);
addDecorator(story => <Provider store={store}>{story()}</Provider>);
addDecorator(story => <MemoryRouter initialEntries={['/']}>{story()}</MemoryRouter>);

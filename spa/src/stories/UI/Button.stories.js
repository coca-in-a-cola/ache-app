import React from 'react';

import { Button } from '../../components/UI/Button';

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: Button,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <Button {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
  children: 'Кнопка',
};

export const Small = Template.bind({});
Small.args = {
  children: 'Маленькая кнопка',
  size: "small",
  className: "",
};

export const Blue = Template.bind({});
Blue.args = {
  children: 'Синяя кнопка',
  className: "bg-blue-darker",
};

export const Timeout = Template.bind({});
Timeout.args = {
  children: 'Кнопка с обратным отсчётом',
  size: "small",
  timeout: 30,
  onClick: () => {alert("Нажата кнопка!")}
};
import React from 'react';

import { FlatButton } from '../../components/UI/FlatButton';

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: FlatButton,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {
    color: { control: 'color' },
  },
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <FlatButton {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
  children: 'Кнопка меню с иконкой',
  icon: 'upload/icons/description.svg'
};

export const BlockLevel = Template.bind({});
BlockLevel.args = {
  children: 'Кнопка фиксированной ширины',
  className: "max-w-xl",
  icon: 'upload/icons/description.svg'
};

export const Red = Template.bind({});
Red.args = {
  children: 'Кнопка с главного меню',
  icon: 'upload/icons/description.svg',
  className: "w-1/3",
  color: "#e41b43"
};
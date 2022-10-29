import React from 'react';

import { ArrowButton } from '../../components/UI/ArrowButton';

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: ArrowButton,
  argTypes: {
    color: { control: 'color' },
  },
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <ArrowButton {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
};

export const Left = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Left.args = {
  left: true
};

export const Colored = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Colored.args = {
  color: '#e21b43'
};
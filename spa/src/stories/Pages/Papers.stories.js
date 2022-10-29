import React from 'react';

import { Papers } from '../../components/Pages/Papers';
// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: Papers,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <Papers {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {};
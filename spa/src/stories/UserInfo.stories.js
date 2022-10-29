import React from 'react';

import { UserInfo } from '../components/UserInfo';
// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: UserInfo,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <UserInfo {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {};
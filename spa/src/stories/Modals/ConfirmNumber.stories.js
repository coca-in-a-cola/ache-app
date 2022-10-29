import React from 'react';

import { ConfirmNumber } from '../../components/Modals/ConfirmNumber'
import { Modal } from '../../components/Modals/Modal';
import { SuccessOrFailReport } from '../../components/UI/SuccessOrFailReport'

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: ConfirmNumber,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <Modal><ConfirmNumber {...args} /></Modal>;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
    onSubmit: (number) => alert("Введён код подтверждения " + number),
    onCancel: () => alert("Пользователь отменил ввод"),
    onRetry: () => alert("Пользователь запросил код снова")
};

const WithFailTemplate = (args) => <Modal>
    <SuccessOrFailReport 
    label={"Введён неверный код подтверждения"}
    fail
    >
    </SuccessOrFailReport>
    <ConfirmNumber {...args} />
  </Modal>;

export const WithFail = WithFailTemplate.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
WithFail.args = {
    onSubmit: (number) => alert("Введён код подтверждения " + number),
    onCancel: () => alert("Пользователь отменил ввод"),
    onRetry: () => alert("Пользователь запросил код снова")
};
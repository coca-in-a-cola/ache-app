import React from 'react';

import { SuccessOrFailReport } from '../../components/UI/SuccessOrFailReport';

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: SuccessOrFailReport,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <SuccessOrFailReport {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
  label: 'Ваша заявка № ХХХХХХХХХХ сформирована',
  text: `По готовности придет смс-сообщение.
  Выдача документов осуществляется в отделе кадров
  с пн. по пт. с 8.00 до 17.00, обед с 11.00 до 12.00
  пл. РЗХМ - каб. 101, пл. ВСП - каб. 103, пл. 1А - каб. 107.`
};

export const Fail = Template.bind({});
Fail.args = {
  fail: true,
  label: 'Произошла ошибка при формировании заявки',
  text: `Приносим извинения за предоставленные неудобства.
  Телефон первой линии: 8 (8342) 38-07-38 доб. 000.
  Код ошибки: 404 - не найдена отправляемая форма`
};

export const Large = Template.bind({});
Large.args = {
  large: true,
  label: 'Ваша заявка № ХХХХХХХХХХ сформирована',
  text: `По готовности придет смс-сообщение.
  Выдача документов осуществляется в отделе кадров
  с пн. по пт. с 8.00 до 17.00, обед с 11.00 до 12.00
  пл. РЗХМ - каб. 101, пл. ВСП - каб. 103, пл. 1А - каб. 107.`
};

export const LargeFail = Template.bind({});
LargeFail.args = {
  large: true,
  fail: true,
  label: 'Произошла ошибка при формировании заявки',
  text: `Приносим извинения за предоставленные неудобства.
  Телефон первой линии: 8 (8342) 38-07-38 доб. 000.
  Код ошибки: 404 - не найдена отправляемая форма`
};
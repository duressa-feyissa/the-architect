"use client";
import { pricing } from "@/utils/constant";
import React, { useState } from "react";
import useTranslation from "next-translate/useTranslation";

function Pricing() {
  const [x, setx] = useState(true);
  const { t } = useTranslation("common");

  return (
    <section className="" data-aos="zoom-y-out">
      <div
        className="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6"
        data-aos="zoom-y-out"
      >
        <div
          className="mx-auto max-w-screen-md text-center mb-8 lg:mb-12"
          data-aos="zoom-y-out"
        >
          <h2
            className="mb-4 text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white"
            data-aos="zoom-y-out"
          >
            {t("pr_header_1")} <br /> {t("pr_header_2")}
          </h2>
          <p
            className="mb-5 font-light text-gray-500 sm:text-xl dark:text-gray-400"
            data-aos="zoom-y-out"
          >
            {t("pr_header_desc")}
          </p>

          <div
            className="flex items-center justify-center mt-10 space-x-4"
            data-aos="zoom-y-out"
          >
            <span className="text-base font-medium">USD</span>
            <button
              className="relative rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              onClick={(e) => setx(!x)}
            >
              <div className="w-16 h-8 transition bg-indigo-500 rounded-full shadow-md outline-none"></div>
              <div
                className={`absolute inline-flex items-center justify-center w-6 h-6 transition-all duration-200 ease-in-out transform bg-white rounded-full shadow-sm top-1 left-1 ${
                  x ? "translate-x-0" : "translate-x-8"
                }`}
              ></div>
            </button>
            <span className="text-base font-medium">ETB</span>
          </div>
        </div>
        <div className="space-y-8 lg:grid lg:grid-cols-2 sm:gap-6 xl:gap-10 lg:space-y-0">
          {pricing.map((e, i) => (
            <div
              key={i}
              className="flex flex-col p-6 mx-auto max-w-lg text-center text-gray-900 bg-white rounded-lg border border-gray-500 shadow dark:border-gray-600 xl:p-8 dark:bg-gray-800 dark:text-white"
              data-aos="zoom-y-out"
            >
              <h3 className="mb-4 text-2xl font-semibold">{e.name}</h3>
              <p
                className="font-light text-gray-500 sm:text-lg dark:text-gray-400"
                data-aos="zoom-y-out"
              >
                {e.description}
              </p>
              <div className="flex justify-center items-baseline my-8">
                <span className="mr-2 text-5xl font-extrabold">
                  {i == 3 ? e.price : x ? "$" + e.priceD : e.priceB + " ETB"}
                </span>
                <span className="text-gray-500 dark:text-gray-400">
                  {i != 3 && "/" + e.duration}
                </span>
              </div>
              <ul role="list" className="mb-8 space-y-4 text-left">
                {e.features.map((feature, index) => (
                  <li key={index} className="flex items-center space-x-3">
                    <svg
                      className="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      ></path>
                    </svg>
                    <span data-aos="zoom-y-out">{feature}</span>
                  </li>
                ))}
              </ul>
              <a
                href={i == 0 ? "/auth/signin" : "/subscribe"}
                className=" bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:ring-primary-200 rounded-lg text-sm px-5 py-2.5 text-center  dark:focus:ring-primary-900 border hover:bg-blue-600 bg-blue-500 font-extrabold"
                data-aos="zoom-y-out"
              >
                {t("pr_action")}
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Pricing;

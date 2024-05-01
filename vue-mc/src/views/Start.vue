<script setup>
import { ref } from 'vue';

</script>

<template>
    <div>
        <BlockViewer header="" >
            <div class="surface-section px-4 py-8 md:px-6 lg:px-8">
                <div class="text-700 text-center">
                    <div class="text-blue-600 font-bold mb-3"><i class="pi pi-heart"></i>&nbsp;AI ACROSS APTC</div>
                    <div class="text-900 font-bold text-6xl mb-3">Analytical Science AI</div>
                    <div class="text-700 text-4xl mb-5 text-left">
                        We are inspired by the ability of AI to help tackle the grand challenges in Analytical Science. At APTC, Our scientists and chemists are shedding new light on the frontiers of Chemistry through breakthroughs in machine learning, cloud infrastructure, and data processing and analytics. Together, our aim is to bring new technology and innovation to the analytical community.
                    </div>
                    <div class="text-700 text-4xl mb-5 text-left">
                        Explore how teams at APTC are using AI to accelerate scientific discovery.
                    </div>
                <!--    <Button label="Join Now" icon="pi pi-discord" class="font-bold px-5 py-3 p-button-raised p-button-rounded white-space-nowrap"></Button>   -->
                </div>
            </div>
        </BlockViewer>

        <BlockViewer header="Chem information">
            <div class="grid grid-nogutter surface-section text-800">
                <div class="col-12 md:col-6 overflow-hidden flex justify-content-center">
                    <img src="/demo/images/blocks/hero/hero-1.png" width="600" alt="Image" class="block md:h-full" style="clip-path: polygon(10% 0, 100% 0%, 90% 100%, 0 100%) " />
                </div>
                <div class="col-12 md:col-6 p-6 text-center md:text-left flex align-items-center">
                    <section>
                        <div class="text-6xl text-primary font-bold mb-3">
                            Al based Spectra Prediction: from chemical structure to MS spectra
                        </div>
                        <p class="mt-0 mb-4 text-700 line-height-3 text-2xl">
                            Another tool is just in the opposite way, from the given chemical structure to predict the MS spectra by Al, because million compounds from Metlin are in the training set.The consistency between Al-predicted spectra and experimental data provided substantial support to our analysis.
                        </p>
                        <router-link to="/cfmid" class="layout-topbar-logo">
                            <Button label="Learn More" type="button" class="mr-3 p-button-raised"></Button>
                        </router-link>
                    </section>
                </div>
            </div>
        </BlockViewer>
        <BlockViewer header="Data intelligent">
            <div class="grid grid-nogutter surface-section text-800">
                <div class="col-12 md:col-6 overflow-hidden flex justify-content-center">
                    <img src="/demo/images/blocks/hero/hero-1.png" width="600" alt="Image" class="block md:h-full" style="clip-path: polygon(10% 0, 100% 0%, 90% 100%, 0 100%) " />
                </div>
                <div class="col-12 md:col-6 p-6 text-center md:text-left flex align-items-center">
                    <section>
                        <div class="text-6xl text-primary font-bold mb-3">
                            HRMS based Database and Data Intelligence
                        </div>
                        <p class="mt-0 mb-4 text-700 line-height-3 text-2xl">
                            temp info.
                        </p>
                        <router-link to="/metfrag" class="layout-topbar-logo">
                            <Button label="Learn More" type="button" class="mr-3 p-button-raised"></Button>
                        </router-link>
                    </section>
                </div>
            </div>
        </BlockViewer>
    </div>
</template>

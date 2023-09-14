
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options 
import random
import pickle
import re
from urllib.parse import urlparse, parse_qs

firefox_options = Options()
firefox_options.add_argument("-headless")

urls = ['https://hubermanlab.com/journal-club-with-dr-peter-attia-metformin-for-longevity-and-the-power-of-belief-effects/',
 'https://hubermanlab.com/guest-series-dr-paul-conti-how-to-understand-and-assess-your-mental-health/',
 'https://hubermanlab.com/marc-andreessen-how-risk-taking-innovation-and-artificial-intelligence-transform-human-experience/',
 'https://hubermanlab.com/goal-toolkit-how-to-set-and-achieve-your-goals/',
 'https://hubermanlab.com/dr-david-linden-life-death-and-the-neuroscience-of-your-unique-experience/',
 'https://hubermanlab.com/dr-rena-improving-sexual-and-urological-health-in-males-and-females/',
 'https://hubermanlab.com/ketamine-benefits-and-risks-for-depression-ptsd-and-neuroplasticity/',
 'https://hubermanlab.com/tony-hawk-harnessing-passion-drive-and-persistence-for-lifelong-success/',
 'https://hubermanlab.com/dr-maya-shankar-how-to-shape-your-identity-and-goals/',
 'https://hubermanlab.com/how-to-enhance-performance-and-learning-by-applying-a-growth-mindset/',
 'https://hubermanlab.com/dr-robert-malenka-how-your-brains-reward-circuits-drive-your-choices/',
 'https://hubermanlab.com/science-supported-tools-to-accelerate-your-fitness-goals/',
 'https://hubermanlab.com/dr-jeffrey-goldberg-how-to-improve-your-eye-health-and-offset-vision-loss/',
 'https://hubermanlab.com/tim-ferriss-how-to-learn-better-and-create-your-best-future/',
 'https://hubermanlab.com/the-science-of-mdma-and-its-therapeutic-applications/',
 'https://hubermanlab.com/dr-immordino-yang-how-emotions-and-social-factors-impact-learning/',
 'https://hubermanlab.com/adderall-stimulants-and-modafinil-for-adhd-short-and-long-term-effects/',
 'https://hubermanlab.com/dr-robin-carhart-harris-the-science-of-psychedelics-for-mental-health/',
 'https://hubermanlab.com/dr-susanna-soberg-how-to-use-cold-and-heat-exposure-to-improve-your-health/',
 'https://hubermanlab.com/how-psilocybin-can-rewire-our-brain-its-therapeutic-benefits-and-its-risks/',
 'https://hubermanlab.com/dr-noam-sobel-how-smells-influence-our-hormones-health-and-behavior/',
 'https://hubermanlab.com/science-based-mental-training-and-visualization-for-improved-learning/',
 'https://hubermanlab.com/dr-matthew-macdougall-neuralink-and-technologies-to-enhance-human-brains/',
 'https://hubermanlab.com/the-science-of-healthy-hair-hair-loss-and-how-to-regrow-hair/',
 'https://hubermanlab.com/dr-elissa-epel-control-stress-for-healthy-eating-metabolism-and-aging/',
 'https://hubermanlab.com/leverage-dopamine-to-overcome-procrastination-and-optimize-effort/',
 'https://hubermanlab.com/dr-peter-attia-improve-vitality-emotional-and-physical-health-and-lifespan/',
 'https://hubermanlab.com/dr-satchin-panda-intermittent-fasting-to-improve-health-cognition-and-longevity/',
 'https://hubermanlab.com/how-to-optimize-your-water-quality-and-intake-for-health/',
 'https://hubermanlab.com/dr-oded-rechavi-genes-and-the-inheritance-of-memories-across-generations/',
 'https://hubermanlab.com/dr-andy-galpin-optimal-nutrition-and-supplementation-for-fitness/',
 'https://hubermanlab.com/how-to-breathe-correctly-for-optimal-health-mood-learning-and-performance/',
 'https://hubermanlab.com/guest-series-dr-andy-galpin-maximize-recovery-to-achieve-fitness-and-performance-goals/',
 'https://hubermanlab.com/dr-gina-poe-use-sleep-to-enhance-learning-memory-and-emotional-state/',
 'https://hubermanlab.com/dr-andy-galpin-optimize-your-training-program-for-fitness-and-longevity/',
 'https://hubermanlab.com/how-to-stop-headaches-using-science-based-approaches/',
 'https://hubermanlab.com/dr-andy-galpin-how-to-build-physical-endurance-and-lose-fat/',
 'https://hubermanlab.com/dr-sara-gottfried-how-to-optimize-female-hormone-health-for-vitality-and-longevity/',
 'https://hubermanlab.com/dr-andy-galpin-optimal-protocols-to-build-strength-and-grow-muscles/',
 'https://hubermanlab.com/how-to-optimize-fertility-in-males-and-females/',
 'https://hubermanlab.com/dr-andy-galpin-how-to-assess-improve-all-aspects-of-your-fitness/',
 'https://hubermanlab.com/rick-rubin-how-to-access-your-creativity/',
 'https://hubermanlab.com/developing-a-rational-approach-to-supplementation-for-health-and-performance/',
 'https://hubermanlab.com/dr-sam-harris-using-meditation-to-focus-view-consciousness-and-expand-your-mind/',
 'https://hubermanlab.com/jocko-willink-how-to-become-resilient-forge-your-identity-and-lead-others/',
 'https://hubermanlab.com/the-science-of-creativity-and-how-to-enhance-creative-innovation/',
 'https://hubermanlab.com/dr-kyle-gillett-tools-for-hormone-optimization-in-males/',
 'https://hubermanlab.com/using-caffeine-to-optimize-mental-and-physical-performance/',
 'https://hubermanlab.com/dr-lex-fridman-navigating-conflict-finding-purpose-and-maintaining-drive/',
 'https://hubermanlab.com/dr-chris-palmer-diet-nutrition-for-mental-health/',
 'https://hubermanlab.com/science-based-tools-for-increasing-happiness/',
 'https://hubermanlab.com/dr-layne-norton-the-science-of-eating-for-health-fat-loss-and-lean-muscle/',
 'https://hubermanlab.com/how-meditation-works-and-science-based-effective-meditations/',
 'https://hubermanlab.com/dr-eddie-chang-the-science-of-learning-and-speaking-languages/',
 'https://hubermanlab.com/fitness-toolkit-protocol-and-tools-to-optimize-physical-health/',
 'https://hubermanlab.com/dr-nolan-williams-psychedelics-and-neurostimulation-for-brain-rewiring/',
 'https://hubermanlab.com/the-effects-of-cannabis-marijuana-on-the-brain-and-body/',
 'https://hubermanlab.com/dr-casey-halpern-biology-and-treatments-for-compulsive-eating-and-behaviors/',
 'https://hubermanlab.com/nicotines-effects-on-the-brain-and-body-and-how-to-quit-smoking-or-vaping/',
 'https://hubermanlab.com/dr-david-anderson-the-biology-of-aggression-mating-and-arousal/',
 'https://hubermanlab.com/focus-toolkit-tools-to-improve-your-focus-and-concentration/',
 'https://hubermanlab.com/dr-erich-jarvis-the-neuroscience-of-speech-language-and-music/',
 'https://hubermanlab.com/what-alcohol-does-to-your-body-brain-health/',
 'https://hubermanlab.com/dr-peter-attia-exercise-nutrition-hormones-for-vitality-and-longevity/',
 'https://hubermanlab.com/sleep-toolkit-tools-for-optimizing-sleep-and-sleep-wake-timing/',
 'https://hubermanlab.com/dr-emily-balcetis-tools-for-setting-and-achieving-goals/',
 'https://hubermanlab.com/the-science-and-treatment-of-bipolar-disorder/',
 'https://hubermanlab.com/dr-charles-zuker-the-biology-of-taste-perception-and-sugar-craving/',
 'https://hubermanlab.com/optimize-and-control-your-brain-chemistry-to-improve-health-and-performance/',
 'https://hubermanlab.com/jeff-cavaliere-optimize-your-exercise-program-with-science-based-tools/',
 'https://hubermanlab.com/the-science-and-treatment-of-obsessive-compulsive-disorder/',
 'https://hubermanlab.com/ido-portal-the-science-and-practice-of-movement/',
 'https://hubermanlab.com/improve-flexibility-with-research-supported-stretching-protocols/',
 'https://hubermanlab.com/dr-paul-conti-therapy-treating-trauma-and-other-life-challenges/',
 'https://hubermanlab.com/the-science-and-process-of-healing-from-grief/',
 'https://hubermanlab.com/dr-wendy-suzuki-boost-attention-and-memory-with-science-based-tools/',
 'https://hubermanlab.com/understand-and-improve-memory-using-science-based-tools/',
 'https://hubermanlab.com/understanding-and-controlling-aggression/',
 'https://hubermanlab.com/dr-rhonda-patrick-micronutrients-for-health-and-longevity/',
 'https://hubermanlab.com/the-science-and-health-benefits-of-deliberate-heat-exposure/',
 'https://hubermanlab.com/using-light-sunlight-blue-light-and-red-light-to-optimize-health/',
 'https://hubermanlab.com/how-to-optimize-your-hormones-for-health-and-vitality/',
 'https://hubermanlab.com/using-deliberate-cold-exposure-for-health-and-performance/',
 'https://hubermanlab.com/dr-andy-galpin-how-to-build-strength-muscle-size-and-endurance/',
 'https://hubermanlab.com/controlling-sugar-cravings-and-metabolism-with-science-based-tools/',
 'https://hubermanlab.com/using-salt-to-optimize-mental-and-physical-performance/',
 'https://hubermanlab.com/dr-justin-sonnenburg-how-to-build-maintain-and-repair-gut-health/',
 'https://hubermanlab.com/how-to-enhance-your-gut-microbiome-for-brain-and-overall-health/',
 'https://hubermanlab.com/dr-david-spiegel-using-hypnosis-to-enhance-mental-and-physical-health-and-performance/',
 'https://hubermanlab.com/the-science-of-love-desire-and-attachment/',
 'https://hubermanlab.com/using-play-to-rewire-and-improve-your-brain/',
 'https://hubermanlab.com/optimizing-workspace-for-productivity-focus-and-creativity/',
 'https://hubermanlab.com/dr-alia-crum-science-of-mindsets-for-health-performance/',
 'https://hubermanlab.com/the-science-of-setting-and-achieving-goals/',
 'https://hubermanlab.com/dr-jack-feldman-breathing-for-mental-physical-health-and-performance/',
 'https://hubermanlab.com/the-science-of-making-and-breaking-habits/',
 'https://hubermanlab.com/dr-david-sinclair-the-biology-of-slowing-and-reversing-aging/',
 'https://hubermanlab.com/science-of-social-bonding-in-family-friendship-and-romantic-love/',
 'https://hubermanlab.com/dr-david-berson-your-brains-logic-and-function/',
 'https://hubermanlab.com/erasing-fears-and-traumas-based-on-the-modern-neuroscience-of-fear/',
 'https://hubermanlab.com/dr-david-buss-how-humans-select-and-keep-romantic-partners-in-short-and-long-term/',
 'https://hubermanlab.com/the-science-of-gratitude-and-how-to-build-a-gratitude-practice/',
 'https://hubermanlab.com/time-perception-and-entrainment-by-dopamine-serotonin-and-hormones/',
 'https://hubermanlab.com/dr-duncan-french-how-to-exercise-for-strength-gains-and-hormone-optimization/',
 'https://hubermanlab.com/using-your-nervous-system-to-enhance-your-immune-system/',
 'https://hubermanlab.com/dr-samer-hattar-timing-light-food-exercise-for-better-sleep-energy-mood/',
 'https://hubermanlab.com/nutrients-for-brain-health-and-performance/',
 'https://hubermanlab.com/effects-of-fasting-and-time-restricted-eating-on-fat-loss-and-health/',
 'https://hubermanlab.com/dr-craig-heller-using-temperature-for-performance-brain-and-body-health/',
 'https://hubermanlab.com/controlling-your-dopamine-for-motivation-focus-and-satisfaction/',
 'https://hubermanlab.com/dr-matthew-johnson-psychedelic-medicine/',
 'https://hubermanlab.com/adhd-and-how-anyone-can-improve-their-focus/',
 'https://hubermanlab.com/healthy-eating-and-eating-disorders-anorexia-bulimia-binging/',
 'https://hubermanlab.com/dr-robert-sapolsky-science-of-stress-testosterone-and-free-will/',
 'https://hubermanlab.com/understanding-and-conquering-depression/',
 'https://hubermanlab.com/dr-anna-lembke-understanding-and-treating-addiction/',
 'https://hubermanlab.com/how-to-control-your-sense-of-pain-and-pleasure/',
 'https://hubermanlab.com/dr-matthew-walker-the-science-and-practice-of-perfecting-your-sleep/',
 'https://hubermanlab.com/how-to-optimize-your-brain-body-function-and-health/',
 'https://hubermanlab.com/dr-lex-fridman-machines-creativity-and-love/',
 'https://hubermanlab.com/maximizing-productivity-physical-and-mental-health-with-daily-tools/',
 'https://hubermanlab.com/the-science-of-hearing-balance-and-accelerated-learning/',
 'https://hubermanlab.com/karl-deisseroth-understanding-and-healing-the-mind/',
 'https://hubermanlab.com/how-smell-taste-and-pheromone-like-chemicals-control-you/',
 'https://hubermanlab.com/the-science-of-vision-eye-health-and-seeing-better/',
 'https://hubermanlab.com/how-to-build-endurance-in-your-brain-and-body/',
 'https://hubermanlab.com/science-of-muscle-growth-increasing-strength-and-muscular-recovery/',
 'https://hubermanlab.com/how-to-lose-fat-with-science-based-tools/',
 'https://hubermanlab.com/how-to-learn-skills-faster/',
 'https://hubermanlab.com/supercharge-exercise-performance-and-recovery-with-cooling/',
 'https://hubermanlab.com/using-cortisol-and-adrenaline-to-boost-our-energy-and-immune-system/',
 'https://hubermanlab.com/how-to-control-your-metabolism-by-thyroid-and-growth-hormone/',
 'https://hubermanlab.com/how-our-hormones-control-our-hunger-eating-and-satiety/',
 'https://hubermanlab.com/the-science-of-how-to-optimize-testosterone-and-estrogen/',
 'https://hubermanlab.com/biological-influences-on-sex-sex-differences-and-preferences/',
 'https://hubermanlab.com/the-science-of-emotions-relationships/',
 'https://hubermanlab.com/how-to-increase-motivation-and-drive/',
 'https://hubermanlab.com/how-foods-and-nutrients-control-our-moods/',
 'https://hubermanlab.com/tools-for-managing-stress-and-anxiety/',
 'https://hubermanlab.com/control-pain-and-heal-faster-with-your-brain/',
 'https://hubermanlab.com/optimize-your-learning-and-creativity-with-science-based-tools/',
 'https://hubermanlab.com/using-failures-movement-and-balance-to-learn-faster/',
 'https://hubermanlab.com/how-to-focus-to-change-your-brain/',
 'https://hubermanlab.com/understanding-and-using-dreams-to-learn-and-to-forget/',
 'https://hubermanlab.com/find-your-temperature-minimum-to-defeat-jetlag-shift-work-and-sleeplessness/',
 'https://hubermanlab.com/using-science-to-optimize-sleep-learning-and-metabolism/',
 'https://hubermanlab.com/master-your-sleep-and-be-more-alert-when-awake/',
 'https://hubermanlab.com/how-your-nervous-system-works-and-changes/',
 'https://hubermanlab.com/welcome-to-the-huberman-lab-podcast/']

def get_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return value

with open('urls.txt', 'w') as fp:

    for i in urls:
        browser = webdriver.Firefox(options=firefox_options)

        browser.get(i)

        browser.implicitly_wait(5)

        elem = browser.find_element(By.XPATH,"/html/body/main/div/article/div/div/p[1]/a[1]")
        url = elem.get_attribute("href")
        video_id = get_video_id(url)
        fp.write("%s\n" % video_id)
        browser.quit()